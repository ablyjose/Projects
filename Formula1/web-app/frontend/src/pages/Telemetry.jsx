import React, { useEffect, useState } from 'react';
import { getTelemetry, getEvents } from '../services/api';
import ChartContainer from '../components/ChartContainer';
import InputSelect from '../components/InputSelect';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Telemetry = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [events, setEvents] = useState([]);

    // Form
    const [year, setYear] = useState(2025);
    const [gp, setGp] = useState('Australia');
    const [session, setSession] = useState('Q');
    const [driver1, setDriver1] = useState('NOR');
    const [driver2, setDriver2] = useState('VER');

    useEffect(() => {
        getEvents(year).then(setEvents).catch(console.error);
    }, [year]);

    const fetchData = async () => {
        setLoading(true);
        try {
            const result = await getTelemetry(year, gp, session, driver1, driver2);
            setData(result);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const TelemetryChart = ({ title, dataKey, yLabel, syncId = "telemetryId" }) => (
        <ChartContainer title={title} height={300}>
            {data ? (
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart>
                        <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                        <XAxis dataKey="Distance" type="number" domain={['auto', 'auto']} stroke="var(--text-secondary)" tick={false} />
                        <YAxis stroke="var(--text-secondary)" label={{ value: yLabel, angle: -90, position: 'insideLeft' }} domain={['auto', 'auto']} />
                        <Tooltip
                            labelFormatter={(v) => `Dist: ${Math.round(v)}m`}
                            contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#333' }}
                        />
                        <Legend />
                        {/* Driver 1 */}
                        <Line
                            data={data.Driver1.Telemetry}
                            dataKey={dataKey}
                            name={data.Driver1.Name}
                            stroke={data.Driver1.Color}
                            dot={false}
                            strokeWidth={2}
                        />
                        {/* Driver 2 */}
                        <Line
                            data={data.Driver2.Telemetry}
                            dataKey={dataKey}
                            name={data.Driver2.Name}
                            stroke={data.Driver2.Color}
                            dot={true}
                            strokeWidth={2}
                            strokeDasharray="4 4"
                        />
                    </LineChart>
                </ResponsiveContainer>
            ) : (
                <div className="placeholder-text">Load data to view</div>
            )}
        </ChartContainer>
    );

    return (
        <div className="page-telemetry">
            <header>
                <h1 style={{ fontSize: '2rem', fontWeight: 700 }}>Telemetry Analysis</h1>
            </header>

            <div className="card" style={{ margin: '24px 0' }}>
                <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'end' }}>
                    <InputSelect label="Year" value={year} onChange={setYear} options={[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025].map(y => ({ label: y, value: y }))} />
                    <InputSelect label="Event" value={gp} onChange={setGp} options={events.map(e => ({ label: e.EventName, value: e.EventName }))} />
                    <InputSelect label="Session" value={session} onChange={setSession} options={[{ label: 'Practice 1', value: 'FP1' }, { label: 'Practice 2', value: 'FP2' }, { label: 'Practice 3', value: 'FP3' }, { label: 'Qualifying', value: 'Q' }, { label: 'Sprint', value: 'S' }, { label: 'Race', value: 'R' }]} />

                    <div className="input-group">
                        <label style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Driver 1</label>
                        <input className="input-text" value={driver1} onChange={e => setDriver1(e.target.value)} />
                    </div>
                    <div className="input-group">
                        <label style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Driver 2</label>
                        <input className="input-text" value={driver2} onChange={e => setDriver2(e.target.value)} />
                    </div>

                    <button className="btn btn-primary" onClick={fetchData} disabled={loading}>
                        {loading ? 'Loading...' : 'Compare'}
                    </button>
                </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <TelemetryChart title="Speed Trace" dataKey="Speed" yLabel="km/h" />
                <TelemetryChart title="Throttle & Brake" dataKey="Throttle" yLabel="%" />

                <ChartContainer title="Time Delta" height={250}>
                    {data && data.Delta ? (
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={data.Delta}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                                <XAxis dataKey="Distance" Stroke="var(--text-secondary)" />
                                <YAxis stroke="var(--text-secondary)" label={{ value: 'Delta (s)', angle: -90, position: 'insideLeft' }} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#333' }}
                                    labelFormatter={(v) => `Dist: ${Math.round(v)}m`}
                                />
                                <Line type="monotone" dataKey="Delta" stroke="var(--text-primary)" dot={false} strokeWidth={2} name={`Gap to ${data.Driver1.Name}`} />
                            </LineChart>
                        </ResponsiveContainer>
                    ) : <div className="placeholder-text">Load data to view delta</div>}
                </ChartContainer>
            </div>
            <style>{`
        .input-text {
            background: var(--bg-surface-hover);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 10px 12px;
            border-radius: 8px;
            outline: none;
            width: 80px;
        }
        .placeholder-text {
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary);
        }
      `}</style>
        </div>
    );
};

export default Telemetry;
