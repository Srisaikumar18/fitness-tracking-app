import './WorkoutList.css'
import { Workout } from '../types'

interface WorkoutListProps {
  workouts: Workout[]
  loading: boolean
  onRefresh: () => void
}

function WorkoutList({ workouts, loading, onRefresh }: WorkoutListProps) {
  // Debug: Log workouts data
  console.log('WorkoutList received workouts:', workouts)
  console.log('Number of workouts:', workouts.length)
  if (workouts.length > 0) {
    console.log('First workout:', workouts[0])
    console.log('First workout fields:', {
      id: workouts[0].id,
      user_name: workouts[0].user_name,
      activity: workouts[0].activity,
      duration: workouts[0].duration,
      calories: workouts[0].calories
    })
  }
  
  if (loading) {
    return (
      <div className="workout-list-container">
        <h2>📋 Workout History</h2>
        <div className="loading">⏳ Loading workouts...</div>
      </div>
    )
  }

  return (
    <div className="workout-list-container">
      <div className="list-header">
        <h2>📋 Workout History</h2>
        <button onClick={onRefresh} className="refresh-btn" title="Refresh list">
          🔄 Refresh
        </button>
      </div>

      {workouts.length === 0 ? (
        <div className="empty-state">
          <p>No workouts yet. Add your first workout above! 💪</p>
        </div>
      ) : (
        <>
          <div className="workout-stats">
            <div className="stat">
              <span className="stat-label">Total Workouts:</span>
              <span className="stat-value">{workouts.length}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Total Duration:</span>
              <span className="stat-value">
                {workouts.reduce((sum, w) => sum + (w.duration || 0), 0)} min
              </span>
            </div>
            <div className="stat">
              <span className="stat-label">Total Calories:</span>
              <span className="stat-value">
                {workouts.reduce((sum, w) => sum + (w.calories || 0), 0)} cal
              </span>
            </div>
          </div>

          <div className="workout-table-container">
            <table className="workout-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>User Name</th>
                  <th>Activity</th>
                  <th>Duration (min)</th>
                  <th>Calories</th>
                </tr>
              </thead>
              <tbody>
                {workouts.map((workout, index) => {
                  // Debug each workout row
                  console.log(`Rendering workout ${index + 1}:`, {
                    id: workout.id,
                    user_name: workout.user_name,
                    activity: workout.activity,
                    duration: workout.duration,
                    calories: workout.calories
                  })
                  
                  return (
                    <tr key={workout.id}>
                      <td>{workouts.length - index}</td>
                      <td>{workout.user_name || 'N/A'}</td>
                      <td>
                        <span className="activity-badge">
                          {workout.activity ? workout.activity.toLowerCase() : 'N/A'}
                        </span>
                      </td>
                      <td>{workout.duration || 0}</td>
                      <td>{workout.calories || 0}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  )
}

export default WorkoutList
