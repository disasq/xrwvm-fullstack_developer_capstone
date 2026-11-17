import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';
import Header from '../Header/Header';
import './Dealers.css';

export default function PostReview() {
  const {id} = useParams();
  const [dealer, setDealer] = useState({});
  const [cars, setCars] = useState([]);
  const [error, setError] = useState('');
  const [sending, setSending] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const [details, models] = await Promise.all([
          fetch(`/djangoapp/dealer/${id}`).then(response => response.json()),
          fetch('/djangoapp/get_cars').then(response => response.json())
        ]);
        setDealer(details.dealer[0]);
        setCars(models.CarModels);
      } catch {
        setError('Unable to load the dealer and car models. Please try again.');
      }
    }
    load();
  }, [id]);

  async function submit(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const [make, model] = JSON.parse(form.get('car'));
    setSending(true);
    setError('');
    try {
      const response = await fetch('/djangoapp/add_review', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          dealership: Number(id), review: form.get('review'),
          purchase: true, purchase_date: form.get('purchase_date'),
          car_make: make, car_model: model, car_year: Number(form.get('car_year'))
        })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Unable to post your review.');
      window.location.href = `/dealer/${id}`;
    } catch (failure) {
      setError(failure.message);
      setSending(false);
    }
  }

  return <><Header/><main style={{maxWidth:680, margin:'40px auto', padding:20}}>
    <h1>{dealer.full_name}</h1><h2>Post Review</h2>
    <form onSubmit={submit}>
      <label style={{display:'block', margin:'16px 0'}}>Review
        <textarea name="review" required rows="5" style={{display:'block', width:'100%', padding:10}}/>
      </label>
      <label style={{display:'block', margin:'16px 0'}}>Purchase Date
        <input type="date" name="purchase_date" required style={{display:'block', padding:8}}/>
      </label>
      <label style={{display:'block', margin:'16px 0'}}>Car Make and Model
        <select name="car" required defaultValue="" style={{display:'block', width:'100%', padding:10}}>
          <option value="" disabled>Choose Car Make and Model</option>
          {cars.map((car, index) => <option key={index} value={JSON.stringify([car.CarMake, car.CarModel])}>
            {car.CarMake} {car.CarModel} ({car.Year})
          </option>)}
        </select>
      </label>
      <label style={{display:'block', margin:'16px 0'}}>Car Year
        <input type="number" name="car_year" min="1900" max={new Date().getFullYear()+1} required style={{display:'block', padding:8}}/>
      </label>
      {error && <p role="alert">{error}</p>}
      <button type="submit" className="btn btn-primary" disabled={sending}>{sending ? 'Posting...' : 'Post Review'}</button>
    </form>
  </main></>;
}
