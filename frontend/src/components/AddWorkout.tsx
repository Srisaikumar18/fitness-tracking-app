import { useState } from 'react'
import './AddWorkout.css'
import { WorkoutCreate } from '../types'

interface AddWorkoutProps {
  onAddWorkout: (workoutData: WorkoutCreate) => Promise<{ success: boolean; error?: string }>
}

function AddWorkout({ onAddWorkout }: AddWorkoutProps) {
  const [formData, setFormData] = useState<WorkoutCreate>({
    user_name: '',
    activity: '',
    duration: 0
  })
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'duration' ? parseInt(value) || 0 : value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validation
    if (!formData.user_name.trim()) {
      setMessage({ type: 'error', text: 'Please enter your name' })
      return
    }
    if (!formData.activity.trim()) {
      setMessage({ type: 'error', text: 'Please enter an activity' })
      return
    }
    if (formData.duration <= 0) {
      setMessage({ type: 'error', text: 'Duration must be greater than 0' })
      return
    }

    setSubmitting(true)
    setMessage(null)

    const result = await onAddWorkout(formData)

    if (result.success) {
      setMessage({ type: 'success', text: '✅ Workout added successfully!' })
      // Clear form
      setFormData({
        user_name: '',
        activity: '',
        duration: 0
      })
      // Clear success message after 3 seconds
      setTimeout(() => setMessage(null), 3000)
    } else {
      setMessage({ type: 'error', text: `❌ ${result.error}` })
    }

    setSubmitting(false)
  }

  return (
    <div className="add-workout-container">
      <h2>➕ Add New Workout</h2>
      
      <form onSubmit={handleSubmit} className="workout-form">
        <div className="form-group">
          <label htmlFor="user_name">Your Name:</label>
          <input
            type="text"
            id="user_name"
            name="user_name"
            value={formData.user_name}
            onChange={handleChange}
            placeholder="Enter your name"
            maxLength={100}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="activity">Activity:</label>
          <input
            type="text"
            id="activity"
            name="activity"
            value={formData.activity}
            onChange={handleChange}
            placeholder="e.g., Running, Cycling, Swimming"
            maxLength={100}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="duration">Duration (minutes):</label>
          <input
            type="number"
            id="duration"
            name="duration"
            value={formData.duration || ''}
            onChange={handleChange}
            placeholder="0"
            min="1"
            required
          />
          <small className="form-hint">
            Calories will be calculated automatically based on activity type
          </small>
        </div>

        {message && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}

        <button 
          type="submit" 
          className="submit-btn"
          disabled={submitting}
        >
          {submitting ? '⏳ Adding...' : '➕ Add Workout'}
        </button>
      </form>
    </div>
  )
}

export default AddWorkout
