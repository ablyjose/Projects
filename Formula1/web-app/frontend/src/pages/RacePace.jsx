import React, { useEffect, useState } from 'react';
import { getRacePace, getEvents } from '../services/api';
import ChartContainer from '../components/ChartContainer';
import InputSelect from '../components/InputSelect';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const RacePace = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [events, setEvents] = useState([]);

    // Form State
    const [year, setYear] = useState(2025);
    const [gp, setGp] = useState('Australia');
    const [session, setSession] = useState('R');
    const [drivers, setDrivers] = useState('NOR, VER');

    useEffect(() => {
        getEvents(year).then(setEvents).catch(console.error);
    }, [year]);

    const fetchData = async () => {
        setLoading(true);
        try {
            const result = await getRacePace(year, gp, session, drivers);
            setData(result);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    // Transform data for Recharts if needed, or use multiple Lines with their own data.
    // We'll use multiple Lines, but we need a common X-axis domain or just one dataset if laps align.
    // For race pace, laps usually align. Let's merge them for the Tooltip to work nicely.

    const processDataForChart = () => {
        if (!data.length) return [];

        // Find max laps
        const maxLaps = Math.max(...data.map(d => d.Laps.length));
        const chartData = [];

        for (let i = 1; i <= maxLaps; i++) {
            const point = { Lap: i };
            data.forEach(d => {
                const lapParams = d.Laps.find(l => l.LapNumber === i);
                if (lapParams) {
                    point[d.Driver] = lapParams.LapTime;
                }
            });
            chartData.push(point);
        }
        return chartData;
    };

    const chartData = processDataForChart();

    return (
        <div className="page-race-pace">
            <header style={{ marginBottom: '24px' }}>
                <h1 style={{ fontSize: '2rem', fontWeight: 700 }}>Race Pace Simulation</h1>
            </header>

            <div className="card" style={{ marginBottom: '24px' }}>
                <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'end' }}>
                    <InputSelect
                        label="Year"
                        value={year}
                        onChange={setYear}
                        options={[2025, 2024, 2023].map(y => ({ label: y, value: y }))}
                    />
                    <InputSelect
                        label="Grand Prix"
                        value={gp}
                        onChange={setGp}
                        options={events.map(e => ({ label: e.EventName, value: e.EventName }))}
                    />
                    <InputSelect
                        label="Session"
                        value={session}
                        onChange={setSession}
                        options={[
                            { label: 'Race', value: 'R' },
                            { label: 'Sprint', value: 'S' },
                            { label: 'Qualifying', value: 'Q' }
                        ]}
                    />
                    <div className="input-group" style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        <label style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Drivers (comma sep)</label>
                        <input
                            type="text"
                            value={drivers}
                            onChange={(e) => setDrivers(e.target.value)}
                            style={{
                                background: 'var(--bg-surface-hover)',
                                border: '1px solid var(--border-color)',
                                color: 'var(--text-primary)',
                                padding: '10px 12px',
                                borderRadius: '8px',
                                outline: 'none',
                                minWidth: '200px',
                                fontFamily: 'inherit'
                            }}
                        />
                    </div>
                    <button className="btn btn-primary" onClick={fetchData} disabled={loading}>
                        {loading ? 'Analyze...' : 'Analyze'}
                    </button>
                </div>
            </div>

            <ChartContainer title={`Lap Times Comparison - ${gp} ${year}`}>
                {chartData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                            <XAxis dataKey="Lap" stroke="var(--text-secondary)" />
                            <YAxis domain={['auto', 'auto']} stroke="var(--text-secondary)" label={{ value: 'Time (s)', angle: -90, position: 'insideLeft' }} />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#333' }}
                                itemStyle={{ color: '#fff' }}
                            />
                            <Legend />
                            {data.map((driverSeries, idx) => (
                                <Line
                                    key={driverSeries.Driver}
                                    type="monotone"
                                    dataKey={driverSeries.Driver}
                                    stroke={driverSeries.Color || `hsl(${idx * 60}, 70%, 50%)`}
                                    strokeWidth={2}
                                    dot={{ r: 3 }}
                                    activeDot={{ r: 6 }}
                                />
                            ))}
                        </LineChart>
                    </ResponsiveContainer>
                ) : (
                    <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}>
                        Select parameters and click Analyze to view data.
                    </div>
                )}
            </ChartContainer>
        </div>
    );
};

export default RacePace;
