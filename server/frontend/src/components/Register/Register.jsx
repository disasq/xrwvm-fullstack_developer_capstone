import React, {useState} from 'react';
import Header from '../Header/Header';
import './Register.css';

export default function Register() {
  const [form, setForm] = useState({userName:'', firstName:'', lastName:'', email:'', password:''});
  const [error, setError] = useState('');
  async function register(event) {
    event.preventDefault();
    const response = await fetch('/djangoapp/register', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(form)});
    const data = await response.json();
    if (!response.ok) {setError(data.error || 'Registration failed'); return;}
    sessionStorage.setItem('username', data.userName);
    sessionStorage.setItem('firstname', data.firstName);
    sessionStorage.setItem('lastname', data.lastName);
    window.location.href = '/';
  }
  return <><Header/><main style={{maxWidth:520, margin:'40px auto'}}><h1>Sign up</h1>
    <form onSubmit={register}>
      {[['userName','Username','text'], ['firstName','First Name','text'], ['lastName','Last Name','text'], ['email','Email','email'], ['password','Password','password']].map(([key,label,type]) =>
        <label key={key} style={{display:'block',margin:'16px 0'}}>{label}<input required type={type} name={key} value={form[key]} onChange={event=>setForm({...form,[key]:event.target.value})} style={{display:'block',width:'100%',padding:10}}/></label>)}
      {error && <p role="alert">{error}</p>}<button type="submit" className="btn btn-primary">Register</button>
    </form></main></>;
}
