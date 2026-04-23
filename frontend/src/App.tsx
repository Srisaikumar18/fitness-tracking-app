import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'
import AddWorkout from './components/AddWorkout'
import WorkoutList from './components/WorkoutList'
import { Workout } from './types'

// Base URL for API
const API_URL = 'http://localhost:8000/api/workouts/'

// Configure axios defaults
axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.headers.get['Accept'] = 'application/json'

function App() {
  const [workouts, setWorkouts] = useState<Workout[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Fetch workouts from API
  const fetchWorkouts = async () => {
    try {
      setLoading(true)
      setError(null)
      
      console.log('Fetching workouts from:', API_URL)
      const response = await axios.get(API_URL, {
        headers: {
          'Accept': 'application/json'
        }
      })
      
      console.log('Workouts fetched successfully:', response.data)
      setWorkouts(response.data)
    } catch (err: any) {
      console.error('Error fetching workouts:', err)
      console.error('Error details:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status,
        url: API_URL
      })
      
      if (err.response) {
        // Server responded with error
        setError(`Server error: ${err.response.status} - ${err.response.data?.detail || 'Unknown error'}`)
      } else if (err.request) {
        // Request made but no response
        setError('Cannot connect to backend. Make sure the server is running on http://localhost:8000')
      } else {
        // Something else happened
        setError(`Error: ${err.message}`)
      }
    } finally {
      setLoading(false)
    }
  }

  // Fetch workouts on component mount
  useEffect(() => {
    fetchWorkouts()
  }, [])

  // Handle adding a new workout
  const handleAddWorkout = async (workoutData: any) => {
    try {
      console.log('Adding workout:', workoutData)
      console.log('POST URL:', API_URL)
      
      const response = await axios.post(API_URL, workoutData, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      })
      
      console.log('Workout added successfully:', response.data)
      
      // Refresh the workout list after adding
      await fetchWorkouts()
      
      return { success: true, data: response.data }
    } catch (err: any) {
      console.error('Error adding workout:', err)
      console.error('Error details:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status,
        requestData: workoutData,
        url: API_URL
      })
      
      let errorMessage = 'Failed to add workout'
      
      if (err.response) {
        // Server responded with error
        if (err.response.data?.detail) {
          if (Array.isArray(err.response.data.detail)) {
            // Validation errors
            errorMessage = err.response.data.detail.map((e: any) => 
              `${e.loc?.join('.')}: ${e.msg}`
            ).join(', ')
          } else {
            errorMessage = err.response.data.detail
          }
        } else {
          errorMessage = `Server error: ${err.response.status}`
        }
      } else if (err.request) {
        // Request made but no response
        errorMessage = 'Cannot connect to backend. Make sure the server is running on http://localhost:8000'
      } else {
        errorMessage = err.message
      }
      
      return { 
        success: false, 
        error: errorMessage
      }
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏋️ Fitness Tracking App</h1>
        <p>Track your workouts and stay healthy!</p>
      </header>

      <main className="App-main">
        <div className="container">
          <AddWorkout onAddWorkout={handleAddWorkout} />
          
          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}
          
          <WorkoutList 
            workouts={workouts} 
            loading={loading}
            onRefresh={fetchWorkouts}
          />
        </div>
      </main>

      <footer className="App-footer">
        <p>© 2024 Fitness Tracking App</p>
      </footer>
    </div>
  )
}

export default App
