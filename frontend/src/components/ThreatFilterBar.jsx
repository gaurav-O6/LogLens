import {
    Search,
    ShieldAlert,
    Network,
    Bug
} from "lucide-react";

import "./ThreatFilterBar.css";


function ThreatFilterBar({
    filters,
    setFilters,
    attackTypes,
}) {


    const updateFilter = (key, value) => {

        setFilters({

            ...filters,

            [key]: value,

        });

    };



    return (

        <section className="threat-filter-bar">



            {/* Search */}

            <div className="filter-search">


                <Search size={18}/>


                <input

                    type="text"

                    placeholder="IP or endpoint..."

                    value={filters.search}

                    onChange={(e)=>
                        updateFilter(
                            "search",
                            e.target.value
                        )
                    }

                />


            </div>





            {/* Severity */}

            <div className="filter-item">


                <ShieldAlert size={18}/>


                <select

                    value={filters.severity}

                    onChange={(e)=>
                        updateFilter(
                            "severity",
                            e.target.value
                        )
                    }

                >

                    <option value="All">
                        All Severities
                    </option>

                    <option value="High">
                        High
                    </option>

                    <option value="Medium">
                        Medium
                    </option>

                    <option value="Low">
                        Low
                    </option>


                </select>


            </div>





            {/* Network */}

            <div className="filter-item">


                <Network size={18}/>


                <select

                    value={filters.network}

                    onChange={(e)=>
                        updateFilter(
                            "network",
                            e.target.value
                        )
                    }

                >

                    <option value="All">
                        All Networks
                    </option>

                    <option value="Internal">
                        Internal
                    </option>

                    <option value="External">
                        External
                    </option>


                </select>


            </div>





            {/* Attack Type */}

            <div className="filter-item">


                <Bug size={18}/>


                <select

                    value={filters.attackType}

                    onChange={(e)=>
                        updateFilter(
                            "attackType",
                            e.target.value
                        )
                    }

                >

                    <option value="All">
                        All Attack Types
                    </option>


                    {
                        attackTypes.map(
                            attack => (

                                <option

                                    key={attack}

                                    value={attack}

                                >

                                    {attack}

                                </option>

                            )
                        )
                    }


                </select>


            </div>



        </section>

    );

}


export default ThreatFilterBar;