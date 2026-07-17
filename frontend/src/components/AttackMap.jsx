import {
    MapContainer,
    TileLayer,
    Marker,
    Popup,
} from "react-leaflet";

import MarkerClusterGroup from "react-leaflet-cluster";

import L from "leaflet";

import {
    Globe,
    ShieldAlert,
    Activity,
    MapPin,
} from "lucide-react";


import "leaflet/dist/leaflet.css";
import "leaflet-defaulticon-compatibility";

import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";

import "./AttackMap.css";



const highIcon = new L.DivIcon({
    className: "severity-marker",
    html: '<div class="marker high"></div>',
    iconSize:[20,20],
});


const mediumIcon = new L.DivIcon({
    className:"severity-marker",
    html:'<div class="marker medium"></div>',
    iconSize:[20,20],
});


const lowIcon = new L.DivIcon({
    className:"severity-marker",
    html:'<div class="marker low"></div>',
    iconSize:[20,20],
});



function getMarkerIcon(severity){

    switch(severity?.toLowerCase()){

        case "high":
            return highIcon;

        case "medium":
            return mediumIcon;

        default:
            return lowIcon;

    }

}



function AttackMap({detections}){


    const locations =
        detections.filter(
            item =>
                item.latitude !== null &&
                item.longitude !== null
        );



    const countries =
        new Set(
            locations.map(
                item=>item.country
            )
        ).size;



    const externalSources =
        locations.filter(
            item=>item.is_private_ip === false
        ).length;



    return (

        <div className="attack-map-container">


            <div className="map-header">


                <div>

                    <h2>
                        Global Attack Map
                    </h2>


                    <p>
                        Geographic intelligence from detected threats
                    </p>

                </div>



                <div className="map-stats">


                    <div>

                        <ShieldAlert size={18}/>

                        <span>
                            {locations.length} Attacks
                        </span>

                    </div>



                    <div>

                        <Globe size={18}/>

                        <span>
                            {countries} Countries
                        </span>

                    </div>



                    <div>

                        <Activity size={18}/>

                        <span>
                            {externalSources} External
                        </span>

                    </div>


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

                    center={[20,0]}

                    zoom={2}

                    scrollWheelZoom={true}

                    className="attack-map"

                >


                    <TileLayer

                        attribution="&copy; OpenStreetMap contributors"

                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"

                    />



                    <MarkerClusterGroup
                        chunkedLoading
                    >


                    {
                        locations.map(
                            attack =>

                            (

                            <Marker

                                key={attack.id}

                                position={[
                                    attack.latitude,
                                    attack.longitude
                                ]}

                                icon={
                                    getMarkerIcon(
                                        attack.severity
                                    )
                                }

                            >


                            <Popup>


                                <div className="attack-popup">


                                    <h3>

                                        {attack.attack_type}

                                    </h3>



                                    <div className={`popup-risk ${attack.severity.toLowerCase()}`}>

                                        <ShieldAlert size={15}/>

                                        {attack.severity} Risk

                                    </div>




                                    <div className="popup-row">

                                        <MapPin size={14}/>

                                        {attack.city || "Unknown"},
                                        {" "}
                                        {attack.country || "Unknown"}

                                    </div>



                                    <div className="popup-item">

                                        <b>
                                            Source
                                        </b>

                                        <span>
                                            {attack.source_ip}
                                        </span>

                                    </div>



                                    <div className="popup-item">

                                        <b>
                                            Target
                                        </b>

                                        <span>
                                            {attack.request_path}
                                        </span>

                                    </div>



                                    <div className="popup-item">

                                        <b>
                                            Pattern
                                        </b>

                                        <span>
                                            {attack.matched_pattern}
                                        </span>

                                    </div>



                                    <div className="popup-item">

                                        <b>
                                            Time
                                        </b>

                                        <span>
                                            {attack.timestamp}
                                        </span>

                                    </div>



                                </div>


                            </Popup>


                            </Marker>

                            )

                        )
                    }


                    </MarkerClusterGroup>


                </MapContainer>

                )

            }


        </div>

    );

}


export default AttackMap;