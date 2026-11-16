const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const Reviews = require('./review');
const Dealerships = require('./dealership');
const app = express();
app.use(cors());
app.use(express.json());
const route = fn => (req, res) => Promise.resolve(fn(req, res)).catch(error => {
  console.error(error.message);
  res.status(500).json({error: 'Database operation failed'});
});
app.get('/', (req, res) => res.json({status: 'ok'}));
app.get('/fetchReviews', route(async (req, res) => res.json(await Reviews.find().lean())));
app.get('/fetchReviews/dealer/:id', route(async (req, res) => res.json(await Reviews.find({dealership: Number(req.params.id)}).sort({id: -1}).lean())));
app.get('/fetchDealers', route(async (req, res) => res.json(await Dealerships.find().sort({id: 1}).lean())));
app.get('/fetchDealers/:state', route(async (req, res) => res.json(await Dealerships.find(req.params.state === 'All' ? {} : {state: req.params.state}).sort({id: 1}).lean())));
app.get('/fetchDealer/:id', route(async (req, res) => res.json(await Dealerships.find({id: Number(req.params.id)}).lean())));
const counterSchema = new mongoose.Schema({_id: String, seq: Number});
const Counter = mongoose.model('Counter', counterSchema);
app.post('/insert_review', route(async (req, res) => {
  const data = req.body;
  const fields = ['dealership', 'review', 'purchase_date', 'car_make', 'car_model', 'car_year', 'name'];
  if (!fields.every(field => data[field])) return res.status(400).json({error: 'Missing review fields'});
  if (!(await Dealerships.exists({id: Number(data.dealership)}))) return res.status(404).json({error: 'Dealer not found'});
  const counter = await Counter.findByIdAndUpdate('reviews', {$inc: {seq: 1}}, {new: true});
  const review = await Reviews.create({...Object.fromEntries(fields.map(key => [key, data[key]])), purchase: Boolean(data.purchase), id: counter.seq});
  res.status(201).json(review);
}));
async function start() {
  await mongoose.connect(process.env.MONGO_URL || 'mongodb://localhost:27017/dealershipsDB');
  for (const [model, file, key] of [[Reviews, 'reviews.json', 'reviews'], [Dealerships, 'dealerships.json', 'dealerships']]) {
    if (await model.countDocuments() === 0) await model.insertMany(JSON.parse(fs.readFileSync(path.join(__dirname, 'data', file)))[key]);
  }
  const latest = await Reviews.findOne().sort({id: -1});
  await Counter.updateOne({_id: 'reviews'}, {$max: {seq: latest ? latest.id : 0}}, {upsert: true});
  app.listen(3030, '0.0.0.0', () => console.log('Express API running on port 3030'));
}
start().catch(error => {console.error(error); process.exit(1);});
