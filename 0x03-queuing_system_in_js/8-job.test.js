import chai from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

chai.should();

describe('createPushNotificationsJobs', () => {
  let queue;

  before(() => {
    // Set up the queue in test mode
    queue = kue.createQueue({ redis: { db: 3 } }); // Use a different Redis DB for testing
    queue.testMode.enter();
  });

  after(() => {
  // Clear the queue and exit test mode
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should display an error message if jobs is not an array', () => {
  // Test the error case
    chai.expect(() => createPushNotificationsJobs('not_an_array', queue)).to.throw(Error);
  });

  it('should create two new jobs to the queue', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
	message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    queue.testMode.jobs.length.should.equal(2);
  });
});
