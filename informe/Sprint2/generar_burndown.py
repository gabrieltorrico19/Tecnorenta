import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

days = [1, 3, 6, 9, 12, 15, 21]
remaining = [24, 22, 18, 14, 9, 5, 0]
ideal = [24, 20, 16, 12, 8, 4, 0]

plt.figure(figsize=(8, 5))
plt.plot(days, remaining, 'o-', color='#E74C3C', linewidth=2.5, markersize=8, label='Trabajo Real')
plt.plot(days, ideal, '--', color='#2F5496', linewidth=2, markersize=6, label='Línea Ideal (Burndown)')

plt.fill_between(days, 0, remaining, alpha=0.08, color='#E74C3C')
plt.fill_between(days, 0, ideal, alpha=0.05, color='#2F5496')

plt.xlabel('Día del Sprint', fontsize=12, fontname='Arial')
plt.ylabel('Tareas Pendientes', fontsize=12, fontname='Arial')
plt.title('Burndown Chart — Sprint 2', fontsize=14, fontname='Arial', fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.3)
plt.xticks(days)
plt.yticks(range(0, 29, 4))
plt.legend(fontsize=11)
plt.xlim(0, 23)
plt.ylim(0, 28)

for d, r in zip(days, remaining):
    plt.annotate(str(r), (d, r), textcoords="offset points", xytext=(0, 12),
                 ha='center', fontsize=9, color='#E74C3C', fontweight='bold')

output = os.path.join(os.path.dirname(__file__), 'capturas', 'burndown_chart.png')
plt.tight_layout()
plt.savefig(output, dpi=150, bbox_inches='tight')
plt.close()
print(f"Burndown chart generado: {output}")
