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

            <input
                type="text"
                placeholder="Search IP, attack type or pattern..."
                value={searchTerm}
                onChange={(event) =>
                    onSearchChange(event.target.value)
                }
            />

            <select
                value={severityFilter}
                onChange={(event) =>
                    onSeverityChange(event.target.value)
                }
            >
                <option value="All">All Severities</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
            </select>

            <select
                value={attackFilter}
                onChange={(event) =>
                    onAttackChange(event.target.value)
                }
            >
                <option value="All">All Attack Types</option>

                {attackOptions.map((attack) => (

                    <option
                        key={attack}
                        value={attack}
                    >
                        {attack}
                    </option>

                ))}

            </select>

        </div>

    );

}

export default ThreatToolbar;