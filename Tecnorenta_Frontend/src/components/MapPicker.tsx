import { useState } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import L, { type LatLng } from "leaflet";

const DEFAULT_CENTER: [number, number] = [-16.5, -68.15];
const DEFAULT_ZOOM = 6;

interface MapPickerProps {
  latitud: number | null;
  longitud: number | null;
  onChange: (lat: number, lng: number) => void;
}

function DraggableMarker({ position, onChange }: { position: LatLng; onChange: (lat: number, lng: number) => void }) {
  const [marker, setMarker] = useState(position);

  useMapEvents({
    click(e) {
      setMarker(e.latlng);
      onChange(e.latlng.lat, e.latlng.lng);
    },
  });

  return (
    <Marker
      draggable
      position={marker}
      eventHandlers={{
        dragend(e) {
          const { lat, lng } = e.target.getLatLng() as LatLng;
          setMarker({ lat, lng } as LatLng);
          onChange(lat, lng);
        },
      }}
    />
  );
}

export default function MapPicker({ latitud, longitud, onChange }: MapPickerProps) {
  const center = latitud && longitud
    ? L.latLng(latitud, longitud)
    : L.latLng(DEFAULT_CENTER[0], DEFAULT_CENTER[1]);

  return (
    <div style={{ borderRadius: "var(--radius-sm)", overflow: "hidden", border: "1px solid var(--border)" }}>
      <MapContainer center={center} zoom={DEFAULT_ZOOM} style={{ height: 300, width: "100%" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <DraggableMarker
          position={center}
          onChange={onChange}
        />
      </MapContainer>
    </div>
  );
}
