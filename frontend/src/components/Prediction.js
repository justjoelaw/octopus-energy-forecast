

const Prediction = ({prediction}) => {
    const energy_type_enum = {
        1: 'gas',
        2: 'electric'
    }

    const energy_unit_enum = {
      1: 'm^3',
      2: 'kWh'
  }

  return (
    <div>
      Predicted {energy_type_enum[prediction.energy_type]} usage: {parseFloat(prediction.sum_predicted_usage).toFixed(2)} {energy_unit_enum[prediction.energy_type]}
    </div>
  )
}

export default Prediction
