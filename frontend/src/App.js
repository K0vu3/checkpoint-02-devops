import React, { useState, useEffect } from 'react';
import { getUsers, createUser, updateUser, deleteUser } from './api';
import './App.css';

function App() {
  const [users, setUsers] = useState([]);
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [email, setEmail] = useState('');
  const [city, setCity] = useState('');
  const [ip, setIP] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    const data = {
      name,
      age: parseInt(age),
      email,
      city,
      ip,
    };

    await createUser(data);
    await getUsersData();
  };

  const getUsersData = async () => {
    const response = await getUsers();
    setUsers(response.data);
  };

  const handleEdit = async (user) => {
    const newName = prompt('Digite o novo nome:', user.name);
    const newAge = parseInt(prompt('Digite o nova idade:', user.age));
    const newEmail = prompt('Digite o novo email:', user.email);
    const newCity = prompt('Digite o nova cidade:', user.city);
    const newIp = prompt('Digite o novo ip:', user.ip);
    if (newName && newAge && newEmail && newCity && newIp) {
      const newData = {
        name: newName,
        age: newAge,
        email: newEmail,
        city: newCity,
        ip: newIp,
      };
      await updateUser(user.id, newData);
      
      await getUsersData();
    }else{
      alert("Ocorreu um erro, por favor preencher todas as informações!")
    }
  };

  const handleDelete = async (user) => {
    const confirmDelete = window.confirm(`Tem certeza de que deseja excluir o usuário ${user.id}?`);
    if (confirmDelete) {
      await deleteUser(user.id);
      await getUsersData();
    }
  };

  useEffect(() => {
    getUsersData();
  }, []);

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
        </label>
        <br />
        <label>
          Age:
          <input type="text" value={age} onChange={(e) => setAge(e.target.value)} />
        </label>
        <br />
        <label>
          Email:
          <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <br />
        <label>
          City:
          <input type="text" value={city} onChange={(e) => setCity(e.target.value)} />
        </label>
        <br />
        <label>
          IP:
          <input type="text" value={ip} onChange={(e) => setIP(e.target.value)} />
        </label>
        <br />
        <button type="submit">Enviar</button>
      </form>
      <br />
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Age</th>
            <th>Email</th>
            <th>City</th>
            <th>IP</th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.name}</td>
              <td>{user.age}</td>
              <td>{user.email}</td>
              <td>{user.city}</td>
              <td>{user.ip}</td>
              <td><button onClick={() => handleEdit(user)}>Editar</button></td>
              <td><button onClick={() => handleDelete(user)}>Deletar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
