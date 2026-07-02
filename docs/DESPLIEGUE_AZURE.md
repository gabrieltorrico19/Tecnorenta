# ☁️ Tutorial de despliegue de SIGTAR en Microsoft Azure

Guía paso a paso para publicar SIGTAR usando un **crédito de USD 100**. La arquitectura
elegida es la más económica y sencilla de operar para este proyecto:

| Componente | Servicio Azure | Plan sugerido | Costo aprox. / mes |
|---|---|---|---|
| Base de datos | **Azure Database for MySQL – Flexible Server** | Burstable **B1ms**, 20 GB | ~USD 12–15 |
| Backend (FastAPI) | **Azure App Service (Linux, Python 3.11)** | **B1** (o F1 gratis para pruebas) | ~USD 13 (F1 = 0) |
| Frontend (React SPA) | **Azure Static Web Apps** | **Free** | USD 0 |
| **Total** | | | **~USD 25–28 / mes** |

> Con USD 100 tienes **~3 meses** de operación continua, o mucho más si apagas los
> servicios cuando no los usas. Para minimizar gasto durante la evaluación: usa **F1**
> (gratis) en App Service y **detén** el servidor MySQL cuando no lo necesites.

---

## 0. Requisitos previos

1. **Redimir el crédito**: entra a <https://www.microsoftazure.com/> o al portal de tu
   código (por ejemplo *Azure for Students*, que suele dar USD 100 sin tarjeta) y activa
   la suscripción. Verifícalo en <https://portal.azure.com> → *Subscriptions*.
2. Instala la **CLI de Azure**: <https://learn.microsoft.com/cli/azure/install-azure-cli>.
3. Autentícate:
   ```bash
   az login
   az account show   # confirma la suscripción con el crédito
   ```
4. Define variables (ajusta el sufijo para que los nombres sean únicos):
   ```bash
   RG=rg-sigtar
   LOC=eastus2
   SUF=$RANDOM
   MYSRV=sigtar-mysql-$SUF
   DBADMIN=sigtaradmin
   DBPASS='Cambia_Esta_Clave_123!'      # 8+ car., mayús/minús/número/símbolo
   DBNAME=tecnorenta
   API=sigtar-api-$SUF
   ```

Crea el grupo de recursos (contenedor lógico de todo):
```bash
az group create -n $RG -l $LOC
```

---

## 1. Base de datos — Azure Database for MySQL (Flexible Server)

```bash
az mysql flexible-server create \
  --resource-group $RG --name $MYSRV --location $LOC \
  --admin-user $DBADMIN --admin-password "$DBPASS" \
  --sku-name Standard_B1ms --tier Burstable \
  --version 8.0.21 --storage-size 20 --public-access 0.0.0.0

az mysql flexible-server db create \
  --resource-group $RG --server-name $MYSRV --database-name $DBNAME
```

- `--public-access 0.0.0.0` crea una regla de firewall que permite **servicios de
  Azure** (tu App Service podrá conectarse). Para correr las migraciones desde **tu PC**,
  añade tu IP:
  ```bash
  MYIP=$(curl -s https://ifconfig.me)
  az mysql flexible-server firewall-rule create -g $RG -n $MYSRV \
    --rule-name mi-pc --start-ip-address $MYIP --end-ip-address $MYIP
  ```
- El host de la base será `"$MYSRV.mysql.database.azure.com"`.
- **Azure MySQL exige SSL.** Descarga el certificado raíz (necesario para conectar):
  ```bash
  curl -o DigiCertGlobalRootCA.crt.pem https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem
  ```

**Cadena de conexión** (formato SQLAlchemy + PyMySQL con SSL):
```
mysql+pymysql://sigtaradmin:Cambia_Esta_Clave_123!@sigtar-mysql-XXXX.mysql.database.azure.com:3306/tecnorenta?ssl_ca=/home/site/DigiCertGlobalRootCA.crt.pem
```
> En App Service el código se despliega en `/home/site/wwwroot`; sube el `.pem` ahí y
> apunta `ssl_ca` a su ruta. Para probar desde tu PC, usa la ruta local del `.pem`.

---

## 2. Ajustes de código necesarios antes de desplegar

Dos cambios pequeños hacen que la app funcione en la nube (ambos son buenas prácticas):

### 2.1 CORS por variable de entorno
En `Tecnorenta_Backend/app/core/config.py` añade un ajuste para los orígenes permitidos:
```python
    CORS_ORIGINS: str = "http://localhost:5173"   # separados por coma
```
Y en `Tecnorenta_Backend/app/main.py` usa ese valor:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)
```
Así podrás autorizar el dominio del frontend (Static Web Apps) sin tocar código.

### 2.2 Archivo de arranque (opcional pero recomendado)
Asegúrate de que `gunicorn` y `uvicorn` estén en `requirements.txt` (uvicorn ya está;
añade `gunicorn>=21.2`). App Service arrancará con el comando que definimos en el paso 3.

> ⚠️ **Fotos de activos:** en App Service el disco local es **efímero** (se borra en cada
> reinicio). Para el demo funciona; para producción, guarda las fotos en **Azure Blob
> Storage**. Es una mejora documentada, no bloqueante para la evaluación.

---

## 3. Backend — Azure App Service (FastAPI)

Crea el plan y la Web App (Python 3.11 en Linux):
```bash
az appservice plan create -g $RG -n plan-sigtar --is-linux --sku B1
az webapp create -g $RG --plan plan-sigtar -n $API --runtime "PYTHON:3.11"
```

Configura las variables de entorno (la app las lee vía Pydantic Settings):
```bash
FRONT_URL="https://<tu-static-web-app>.azurestaticapps.net"   # lo obtienes en el paso 4
az webapp config appsettings set -g $RG -n $API --settings \
  DATABASE_URL="mysql+pymysql://$DBADMIN:$DBPASS@$MYSRV.mysql.database.azure.com:3306/$DBNAME?ssl_ca=/home/site/DigiCertGlobalRootCA.crt.pem" \
  SECRET_KEY="pon-aqui-una-clave-larga-y-secreta" \
  CORS_ORIGINS="$FRONT_URL" \
  SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

Define el **comando de inicio** (Gunicorn con workers Uvicorn):
```bash
az webapp config set -g $RG -n $API \
  --startup-file "gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app.main:app"
```

Despliega el código del backend (desde la carpeta del backend):
```bash
cd Tecnorenta_Backend
# incluye el certificado SSL para que quede en /home/site/wwwroot
zip -r ../backend.zip . -x "venv/*" "__pycache__/*" "*.pyc"
az webapp deploy -g $RG -n $API --src-path ../backend.zip --type zip
```

Sube el certificado y **corre las migraciones + seed** por SSH:
```bash
az webapp ssh -g $RG -n $API
# dentro del contenedor:
cd /home/site/wwwroot
# (sube DigiCertGlobalRootCA.crt.pem a /home/site/ vía FTPS o inclúyelo en el zip)
alembic upgrade head       # crea el esquema Y siembra el demo (migraciones a7c1/b8d2/c9e3)
python -m app.seed         # (opcional) idempotente: roles/permisos/usuarios
python -m app.seed_data    # (opcional) idempotente: datos de negocio
exit
```
> Recuerda: `alembic upgrade head` ya deja la base poblada con el DSS gracias a las tres
> migraciones de datos; `app.seed*` es redundante e idempotente (no duplica).

Verifica el backend:
```bash
curl https://$API.azurewebsites.net/api/v1/health
curl https://$API.azurewebsites.net/api/v1/dashboard/stats
```

---

## 4. Frontend — Azure Static Web Apps (React)

Compila el frontend apuntando a la API publicada:
```bash
cd ../Tecnorenta_Frontend
echo "VITE_API_URL=https://$API.azurewebsites.net/api/v1" > .env.production
npm ci
npm run build     # genera dist/
```

Despliega `dist/` con la CLI de Static Web Apps:
```bash
npm install -g @azure/static-web-apps-cli
SWA=sigtar-web-$SUF
az staticwebapp create -g $RG -n $SWA -l $LOC   # crea el recurso (plan Free)
# token de despliegue:
TOKEN=$(az staticwebapp secrets list -g $RG -n $SWA --query "properties.apiKey" -o tsv)
swa deploy ./dist --deployment-token "$TOKEN" --env production
```

Toma la URL resultante (`https://<SWA>.azurestaticapps.net`) y **actualiza el CORS del
backend** con ella:
```bash
az webapp config appsettings set -g $RG -n $API --settings \
  CORS_ORIGINS="https://$SWA.azurestaticapps.net"
az webapp restart -g $RG -n $API
```

> Alternativa recomendada para producción: conecta el repositorio de GitHub a Static Web
> Apps (Deploy → GitHub). Azure crea un workflow de GitHub Actions que compila y publica
> en cada push a `develop`/`main`.

---

## 5. Verificación end-to-end

1. Abre `https://<SWA>.azurestaticapps.net` → inicia sesión (`gerente@tecnorenta.com` / `demo1234`).
2. El **Dashboard DSS** debe mostrar las 3 franjas con semáforos, tendencia y recomendaciones.
3. Revisa la consola del navegador: no debe haber errores de CORS (si los hay, revisa `CORS_ORIGINS`).
4. `https://<API>.azurewebsites.net/docs` muestra el Swagger de FastAPI.

---

## 6. Control de costos (para que el crédito rinda)

- **Detén** el servidor MySQL cuando no lo uses: `az mysql flexible-server stop -g $RG -n $MYSRV` (y `start` para reanudar). No factura cómputo mientras está detenido (sí el almacenamiento, mínimo).
- Usa **F1 (gratis)** en App Service durante el desarrollo: `az appservice plan update -g $RG -n plan-sigtar --sku F1` (tiene límite de CPU/día; suficiente para demo).
- Vigila el gasto en el portal → *Cost Management* → *Budgets*; crea una alerta a USD 80.
- Al terminar la evaluación, **elimina todo** con un comando:
  ```bash
  az group delete -n $RG --yes --no-wait
  ```

---

## 7. Resumen del flujo

```
Crédito → az login → Resource Group
      → MySQL Flexible (B1ms) + DB + firewall + SSL
      → App Service (Python) : DATABASE_URL, CORS, startup gunicorn/uvicorn → deploy zip → alembic upgrade head
      → Static Web Apps (Free) : build con VITE_API_URL → swa deploy → actualizar CORS
      → Verificar dashboard DSS  ✅
```

Con esto SIGTAR queda accesible públicamente, con base de datos gestionada, backend por
capas y frontend SPA, dentro del presupuesto del crédito de USD 100.
