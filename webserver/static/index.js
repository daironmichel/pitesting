function moveMotorUp() {
  axios.post('/api/desk/up')
    .then(response => {
      if (response.data.ok) {
        console.log('moving desk up');
      } else {
        console.error('something went wrong!')
      }
    })
    .catch(error => console.error(error));
}

function moveMotorDown() {
  axios.post('/api/desk/down')
    .then(response => {
      if (response.data.ok) {
        console.log('moving desk down');
      } else {
        console.error('something went wrong!')
      }
    })
    .catch(error => console.error(error));
}

function stopMotor() {
  axios.post('/api/desk/stop')
    .then(response => {
      if (response.data.ok) {
        console.log('desk stopped');
      } else {
        console.error('something went wrong!')
      }
    })
    .catch(error => console.error(error));
}
