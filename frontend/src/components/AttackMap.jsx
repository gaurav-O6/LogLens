import {
    MapContainer,
    TileLayer,
    Marker,
    Popup,
} from "react-leaflet";

import L from "leaflet";

import "leaflet/dist/leaflet.css";
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";

import "./AttackMap.css";

const highIcon = new L.DivIcon({
    className: "severity-marker",
    html: '<div class="marker high"></div>',
    iconSize: [18, 18],
});

const mediumIcon = new L.DivIcon({
    className: "severity-marker",
    html: '<div class="marker medium"></div>',
    iconSize: [18, 18],
});

const lowIcon = new L.DivIcon({
    className: "severity-marker",
    html: '<div class="marker low"></div>',
    iconSize: [18, 18],
});

function getMarkerIcon(severity) {

    switch (severity?.toLowerCase()) {

        case "high":
            return highIcon;

        case "medium":
            return mediumIcon;

        default:
            return lowIcon;

    }

}

function AttackMap({ detections }) {

    const locations = detections.filter(
        (item) =>
            item.latitude !== null &&
            item.longitude !== null
    );

    return (

        <div className="attack-map-container">

            <div className="chart-header">

                <div>

                    <h2>
                        Global Attack Map
                    </h2>

                    <p>
                        Geographic origin of detected attacks
                    </p>

                </div>

            </div>

            {

                locations.length === 0 ?

                (

                    <div className="map-empty">

                        No GeoIP locations available.

                    </div>

                )

                :

                (

                    <MapContainer
                        center={[20, 0]}
                        zoom={2}
                        scrollWheelZoom={true}
                        className="attack-map"
                    >

                        <TileLayer
                            attribution='&copy; OpenStreetMap contributors'
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        />

                        {

                            locations.map((attack) => (

                                <Marker
                                    key={attack.id}
                                    position={[
                                        attack.latitude,
                                        attack.longitude,
                                    ]}
                                    icon={getMarkerIcon(attack.severity)}
                                >

                                    <Popup>

                                        <strong>

                                            {attack.attack_type}

                                        </strong>

                                        <br /><br />

                                        <b>Severity:</b>

                                        {" "}

                                        {attack.severity}

                                        <br />

                                        <b>IP:</b>

                                        {" "}

                                        {attack.source_ip}

                                        <br />

                                        <b>Location:</b>

                                        {" "}

                                        {attack.city || "Unknown"}

                                        {", "}

                                        {attack.country || "Unknown"}

                                        <br />

                                        <b>Endpoint:</b>

                                        {" "}

                                        {attack.request_path}

                                        <br />

                                        <b>Time:</b>

                                        {" "}

                                        {attack.timestamp}

                                    </Popup>

                                </Marker>

                            ))

                        }

                    </MapContainer>

                )

            }

        </div>

    );

}

export default AttackMap;