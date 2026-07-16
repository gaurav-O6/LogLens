import {
    Search,
    ShieldAlert,
    Crosshair
} from "lucide-react";


function ThreatToolbar({
    searchTerm,
    onSearchChange,
    severityFilter,
    onSeverityChange,
    attackFilter,
    attackOptions,
    onAttackChange,
}) {


    return (

        <div className="threat-toolbar">


            <div className="toolbar-search">

                <Search size={18}/>


                <input

                    type="text"

                    placeholder="Search IP, attack type or pattern..."

                    value={searchTerm}

                    onChange={(event) =>
                        onSearchChange(event.target.value)
                    }

                />

            </div>





            <div className="toolbar-filter">


                <ShieldAlert size={17}/>


                <select

                    value={severityFilter}

                    onChange={(event)=>
                        onSeverityChange(
                            event.target.value
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






            <div className="toolbar-filter">


                <Crosshair size={17}/>


                <select

                    value={attackFilter}

                    onChange={(event)=>
                        onAttackChange(
                            event.target.value
                        )
                    }

                >

                    <option value="All">

                        All Attack Types

                    </option>



                    {
                        attackOptions.map(
                            (attack)=>(
                                
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



        </div>

    );

}


export default ThreatToolbar;