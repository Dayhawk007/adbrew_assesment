import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const todoApi = "http://localhost:8000/todos/";

export function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await axios.get(todoApi);
      setTodos(response.data);
    } catch (err) {
      console.error("Error fetching todos:", err);
    }
  };

  const handleAddTodo = async (e) => {
    e.preventDefault();
    if (!newTodo.trim()) {
      setError('Todo cannot be empty');
      return;
    }

    try {
      const response = await axios.post(todoApi, { title: newTodo });
      setTodos(response.data);
      setNewTodo('');
      setError('');
    } catch (err) {
      console.error("Error adding todo:", err);
      setError('Failed to add todo');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-gray-800 p-6 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold mb-6 text-center">List of TODOs</h1>
        <ul className="mb-8 space-y-2">
          {todos.map((todo, index) => (
            <li key={index} className="bg-gray-700 p-4 rounded shadow">
              {todo.title}
            </li>
          ))}
        </ul>
        <h1 className="text-3xl font-bold mb-4 text-center">Create a ToDo</h1>
        <form onSubmit={handleAddTodo} className="space-y-4">
          <div>
            <label htmlFor="todo" className="block text-sm font-medium mb-2">ToDo:</label>
            <input
              type="text"
              id="todo"
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              className="w-full p-2 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-gray-400"
            />
            {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
          </div>
          <div>
            <button type="submit" className="w-full p-2 bg-blue-600 rounded hover:bg-blue-500 focus:outline-none focus:bg-blue-700">
              Add ToDo!
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
