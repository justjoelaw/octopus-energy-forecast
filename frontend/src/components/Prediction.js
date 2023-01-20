

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

  return (
    <div>
      Predicted {energy_type_enum[prediction.energy_type]} usage: {parseFloat(prediction.sum_predicted_usage).toFixed(2)} {energy_unit_enum[prediction.energy_type]}
      <br />
      Your predicted daily {energy_type_enum[prediction.energy_type]} usage this week is {parseFloat(prediction.sum_predicted_usage / 7).toFixed(2)}{energy_unit_enum[prediction.energy_type]} compared to your average of {calculate_historic_average(historic)}{energy_unit_enum[prediction.energy_type]}.
      This represents a
      <span style={{ fontWeight: 'bold' }}> {parseFloat((((prediction.sum_predicted_usage / 7) - calculate_historic_average(historic)) / calculate_historic_average(historic)) *100).toFixed(2)}% </span>
      change
    </div>
  )
}

export default Prediction
