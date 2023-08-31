import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const app = express();
const port = 1245;

const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Initialize available seat and reservation status
const initialAvailableSeats = 50;
let reservationEnabled = true;
setAsync('available_seats', initialAvailableSeats);

const queue = kue.createQueue();

// Function to reserve a seat
function reserveSeat(number) {
  return setAsync('available_seats', number);
}

// Async fucntion to get current available seats
async function getCurrentAvailableSeats() {
  const availableSeats = await getAsync('available_seats');
  return parseInt(availableSeats) || 0;
}

// middleware to handle JSON response
app.use(express.json());

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat', {}).save(err => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });
});

app.get('/process', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
	  
  queue.process('reserve_seat', async (job, done) => {
    const newAvailableSeats = numberOfAvailableSeats - 1;
    if (newAvailableSeats >= 0) {
      await reserveSeat(newAvailableSeats);
      if (newAvailableSeats === 0) {
        reservationEnabled = false;
      }
      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });

  res.json({ status: 'Queue processing' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
