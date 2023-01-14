import {useState, useEffect} from 'react'
import Button from './components/Button'
import Plot from './components/Plot'
import Prediction from './components/Prediction'

function App() {

  const [historicPlots, setHistoricPlots] = useState([])

  const [showPredictions, setShowPredictions] = useState(false)

  const [electricPrediction, setElectricPrediction] = useState(null)
  const [electricPredictionPlot, setElectricPredictionPlot] = useState(null)

  const [gasPrediction, setGasPrediction] = useState(null)
  const [gasPredictionPlot, setGasPredictionPlot] = useState(null)


  useEffect(() => {
    const getLatestPlots = async () => {
      const latestPlots = await fetchPlotListLatest()
      setHistoricPlots(latestPlots)
      console.log(latestPlots)
      return latestPlots
    }

    // Create latest plots
    const createLatestPlots = async () => {
      await updateGas()
      await updateElectric()
      await updateWeather()
      const latest_gas_result = await generatePlot('gas')
      const latest_electric_result = await generatePlot('electric')
      setHistoricPlots([latest_gas_result['plot'], latest_electric_result['plot']])

    }


  getLatestPlots()
  .then((latestPlots) => {
    
    if (latestPlots.length < 2) {
      createLatestPlots()
    }
  })

  }, [])

  // Fetch latest plots
  const fetchPlotListLatest = async () => {
    const res = await fetch('/api/plots?latest_only=true')
    const data = await res.json()

    return data
  }

  // Update Gas
  const updateGas = async () => {
    const res = await fetch('/api/update_gas', {
    method: 'POST'
    })
    console.log(await res.text())
  }

  // Update Electric
  const updateElectric = async () => {
    const res = await fetch('/api/update_electric', {
    method: 'POST'
    })
    console.log(await res.text())
  }

  // Update Weather
  const updateWeather = async () => {
    const res = await fetch('/api/update_weather', {
    method: 'POST'
    })
    console.log(await res.text())
  }

  // Generate Plot
  const generatePlot = async (plot_type, prediction_on='') => {
    const res = await fetch('/api/generate_plot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          'plot_type': plot_type,
          'prediction_on': prediction_on
      })
    })
    const result = await res.json()
    console.log(result)
    return result
  }

  // Show Predictions
  const createAndShowPredictions = async () => {
  
    setShowPredictions(true)

    const result_electric = await generatePlot('prediction', 'electric')
    setElectricPrediction(await result_electric['prediction'])
    setElectricPredictionPlot(await result_electric['plot'])

    const result_gas = await generatePlot('prediction', 'gas')
    setGasPrediction(await result_gas['prediction'])
    setGasPredictionPlot(await result_gas['plot']) 



  }



  return (
    <div className="container">
      <h1>Octopus Energy: Forecast</h1>
      <p>A simple project which combines data from the Octopus Energy API, with data from "weatherapi", to:</p>
      <ul>
          <li>Show energy usage for the past 60 days, plotted against average daily temperature</li>
          <li>Predict energy usage over the next 7 days, by running a simple linear regression based on forecasted daily average temperate, and day-of-the-week</li>
        </ul> 
        
      <div className='plots-container'>
        {historicPlots.map((plot) => 
        <Plot key={plot.id} plot={plot} />
        )}
      </div>

      <div className='prediction-button-container'>
          <Button text='Generate Energy Forecast' onClick={createAndShowPredictions} />
      </div>

      <div className='prediction-plots-container'>
        { gasPredictionPlot && <Plot key={gasPredictionPlot.id} plot={gasPredictionPlot} />}
        { electricPredictionPlot && <Plot key={electricPredictionPlot.id} plot={electricPredictionPlot} />}
      </div>

      <div className='prediction-container'>
        { gasPrediction && <Prediction key={gasPrediction.id} prediction={gasPrediction} /> }
        { electricPrediction && <Prediction key={electricPrediction.id} prediction={electricPrediction} /> }
      </div>

    </div>
  );
}

export default App;
