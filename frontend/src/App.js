import {useState, useEffect} from 'react'
import Button from './components/Button'
import Plot from './components/Plot'
import Prediction from './components/Prediction'

function App() {

  const csrftoken = getCookie('csrftoken');

  const [historicPlots, setHistoricPlots] = useState([])

  const [showPredictions, setShowPredictions] = useState(false)

  const [electricPrediction, setElectricPrediction] = useState(null)
  const [electricPredictionPlot, setElectricPredictionPlot] = useState(null)

  const [gasPrediction, setGasPrediction] = useState(null)
  const [gasPredictionPlot, setGasPredictionPlot] = useState(null)

  const [gasHistoric, setGasHistoric] = useState(null)
  const [electricHistoric, setElectricHistoric] = useState(null)


  useEffect(() => {
    const getLatestPlots = async () => {
      const latestPlots = await fetchPlotListLatest()
      setHistoricPlots(latestPlots)
      console.log(latestPlots)
      return latestPlots
    }

    // Create latest plots
    const createLatestPlots = async () => {
      await updateGas(csrftoken)
      await updateElectric(csrftoken)
      await updateWeather(csrftoken)
      const latest_gas_result = await generatePlot(csrftoken, 'gas')
      const latest_electric_result = await generatePlot(csrftoken, 'electric')
      setHistoricPlots([latest_gas_result['plot'], latest_electric_result['plot']])

    }


  getLatestPlots()
  .then((latestPlots) => {
    
    if (latestPlots.length < 2) {
      createLatestPlots()
    }
  })

  }, [])

  // Get Cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  // Fetch latest plots
  const fetchPlotListLatest = async () => {
    const res = await fetch('/api/plots?latest_only=true')
    const data = await res.json()

    return data
  }

  // Update Gas
  const updateGas = async (csrftoken) => {
    const res = await fetch('/api/update_gas', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
    })
    console.log(await res.text())
  }

  // Update Electric
  const updateElectric = async (csrftoken) => {
    const res = await fetch('/api/update_electric', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
    })
    console.log(await res.text())
  }

  // Update Weather
  const updateWeather = async (csrftoken) => {
    const res = await fetch('/api/update_weather', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
    })
    console.log(await res.text())
  }

  // Generate Plot
  const generatePlot = async (csrftoken, plot_type, prediction_on='') => {
    const res = await fetch('/api/generate_plot', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
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

  // Get Historic Gas usage
  const getGas = async () => {
    const res = await fetch('/api/gas')
    const data = await res.json()

    return data
  }

  // Get Historic Electric usage
  const getElectric = async () => {
    const res = await fetch('/api/electric')
    const data = await res.json()

    return data
  }

  // Show Predictions
  const createAndShowPredictions = async () => {
  
    setShowPredictions(true)

    const historic_gas = await getGas()
    console.log(await historic_gas)
    setGasHistoric(await historic_gas)
    const historic_electric = await getElectric()
    setElectricHistoric(await historic_electric)

    const result_electric = await generatePlot(csrftoken, 'prediction', 'electric')
    setElectricPrediction(await result_electric['prediction'])
    setElectricPredictionPlot(await result_electric['plot'])

    const result_gas = await generatePlot(csrftoken, 'prediction', 'gas')
    setGasPrediction(await result_gas['prediction'])
    setGasPredictionPlot(await result_gas['plot']) 

  }



  return (
    <div className="container">
      <h1>Octopus Energy: Forecast</h1>
      <p>A project created using Python, Javascript, Django and React. The app is deployed on Heroku, with a postgreSQL database</p>
      <br/>
      <p>My aim with this app was to use data from the Octopus Energy API and combine it with data from 'weatherapi', to:</p>
      <ul>
        <li>Show energy usage for the past 60 days, plotted against average daily temperature</li>
        <li>Predict energy usage over the next 7 days, by running a simple linear regression model with two inputs:</li>
        <ol className='model-inputs'>
          <li>forecasted daily average temperature</li>
          <li>day-of-the-week</li>
        </ol>
      </ul>
      <div className="plots-description">
        <p>These plots show how your gas and electricty consumption has varied over the past 60 days, with the average daily temperature for each day</p>
      </div>
      <div className='plots-container'>
        {historicPlots.map((plot) => 
        <Plot key={plot.id} plot={plot} />
        )}
      </div>

      <div className='prediction-button-container'>
          <Button text='Generate Energy Forecast' onClick={createAndShowPredictions} />
      </div>

      <div className='prediction-description'>
        <p>These plots show the forecasted average daily temperature over the next 7 days, and the amount of energy we expect you to use</p>
      </div>

      <div className='prediction-plots-container'>
        { gasPredictionPlot && <Plot key={gasPredictionPlot.id} plot={gasPredictionPlot} />}
        { electricPredictionPlot && <Plot key={electricPredictionPlot.id} plot={electricPredictionPlot} />}
      </div>

      <div className='prediction-container'>
        { gasPrediction && <Prediction key={gasPrediction.id} prediction={gasPrediction} historic={gasHistoric} /> }
        { electricPrediction && <Prediction key={electricPrediction.id} prediction={electricPrediction} historic={electricHistoric} /> }
      </div>

    </div>
  );
}

export default App;
