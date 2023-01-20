

const Prediction = ({prediction, historic}) => {
    const energy_type_enum = {
        1: 'gas',
        2: 'electric'
    }

    const energy_unit_enum = {
      1: 'm^3',
      2: 'kWh'
  }

    const calculate_historic_average= (historic) => {
      let total = 0
      // console.log(historic)
      for (let row in historic) {
        total += historic[row].consumption
        // console.log(row)
      }

      let result = total / historic.length
      // console.log(total)
      return parseFloat(result).toFixed(2)
    }

    const historic_average = calculate_historic_average(historic)
    const predicted_average = prediction.sum_predicted_usage / 7
    const percent_change_in_average = ((predicted_average - historic_average) / historic_average) * 100


  return (
    <div>
      Predicted {energy_type_enum[prediction.energy_type]} usage: {parseFloat(prediction.sum_predicted_usage).toFixed(2)} {energy_unit_enum[prediction.energy_type]}
      <br />
      Your predicted daily {energy_type_enum[prediction.energy_type]} usage this week is {parseFloat(predicted_average).toFixed(2)}{energy_unit_enum[prediction.energy_type]} compared to your average of {parseFloat(historic_average).toFixed(2)}{energy_unit_enum[prediction.energy_type]}.
      This represents a
      <span style={{ fontWeight: 'bold' }}> {parseFloat(percent_change_in_average).toFixed(2)}% {percent_change_in_average > 0 ? 'increase' : 'descrease'}</span>
    </div>
  )
}

export default Prediction
