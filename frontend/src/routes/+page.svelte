<script>
    import { dev } from "$app/environment";
    let url = location.protocol + "//" + location.host;
    if (dev) {
        url = "http://localhost:5000";
    }

    let wcapt_t = 0; // Jährliche Wassergewinnung (in 1000 m3), Total
    let wcapt_sour = 0; // Jährliche Wassergewinnung (in 1000 m3), Quellwasser
    let wcapt_lac_riv = 0; // Jährliche Wassergewinnung (in 1000 m3), See- und Flusswasser
    let wlivr_moy = 0; // Tägliche Wasserabgabe (m3), Mittel
    let deb_hj_moy = 0; // Liter je Einwohner/in und Tag des Versorgungsgebietes, Mittel
    let gaz_t = 0; // Gasverkauf (in 1000 kWh), Total

    let prediction = "n.a.";

    async function predict() {
    const response = await fetch(`${url}/api/predict_population_class`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            deb_hj_moy: deb_hj_moy,
            gaz_t: gaz_t,
            wcapt_lac_riv: wcapt_lac_riv,
            wcapt_sour: wcapt_sour,
            wcapt_t: wcapt_t,
            wlivr_moy: wlivr_moy,
        })
    });
    if (response.ok) {
        const data = await response.json();
        prediction = `Predicted Population Class: ${data.predicted_class}`;
    } else {
        console.error('Error predicting:', response.statusText);
        prediction = "Error";
    }
}
</script>

<h1>BFS Energie Model Prediction</h1>
<h2>2020 Dataset</h2>

<form on:submit|preventDefault={predict}>
    <p>
        <strong>Jährliche Wassergewinnung (in 1000 m3), Total:</strong>
        <input type="number" bind:value={wcapt_t} min="0" />
    </p>

    <p>
        <strong>Jährliche Wassergewinnung (in 1000 m3), Quellwasser:</strong>
        <input type="number" bind:value={wcapt_sour} min="0" />
    </p>

    <p>
        <strong>Jährliche Wassergewinnung (in 1000 m3), See- und Flusswasser:</strong>
        <input type="number" bind:value={wcapt_lac_riv} min="0" />
    </p>

    <p>
        <strong>Tägliche Wasserabgabe (m3), Mittel:</strong>
        <input type="number" bind:value={wlivr_moy} min="0" />
    </p>

    <p>
        <strong>Liter je Einwohner/in und Tag des Versorgungsgebietes, Mittel:</strong>
        <input type="number" bind:value={deb_hj_moy} min="0" />
    </p>

    <p>
        <strong>Gasverkauf (in 1000 kWh), Total:</strong>
        <input type="number" bind:value={gaz_t} min="0" />
    </p>

    <button type="submit">Predict</button>
</form>

<p>{prediction}</p>


<h2>Populationsklassen</h2>
<table>
    <thead>
        <tr>
            <th>Populationsklasse</th>
            <th>Beschreibung</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Gemeindegrössenklasse mit weniger als 10'000 Einwohnern</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Gemeindegrössenklasse mit 10'000 - 14'999 Einwohnern</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Gemeindegrössenklasse mit 15'000 - 19'999 Einwohnern</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Gemeindegrössenklasse mit 20'000 - 49'999 Einwohnern</td>
        </tr>
    </tbody>
</table>

<style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        text-align: left;
        padding: 8px;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    th {
        background-color: #4890dc;
        color: white;
    }
</style>
