function LoginForm(props) {
    const [formData, setFormData] = React.useState(initialLoginFormData);
    const [error, setError] = React.useState(null);
    let history = useHistory();
  
    const handleChange = (evt) => {
      setFormData({
        ...formData, [evt.target.name]: evt.target.value.trim()
      });
    };
  
    const handleSubmit = (evt) => {
      evt.preventDefault();
      
      fetch('/api/users/login', {
        method: 'POST',
        body: JSON.stringify(formData),
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(res => res.json())
      .then(
        (data) => {
        if (data.status != 'error') {
          props.setUser(data.user);
          localStorage.setItem('user', JSON.stringify(data.user));
          history.push('/');
        } else alert(data.message);
      },
      (error) => {
        setError(error)
      });
    }
  
    return (
      <div className="container border rounded mt-5 col-md-6 p-5" id="login-form">
        <h1>Log In</h1>
          <form onSubmit={handleSubmit}>
  
            <div className="form-group p-2">
              <input type="text" className="form-control" name="username" 
                placeholder="Username" required onChange={handleChange} />
            </div>
  
            <div className="form-group p-2">
              <input type="password" className="form-control" name="password" 
                placeholder="Password" required onChange={handleChange} />
            </div>
  
            <button type="submit" className="btn btn-primary">Log In</button>
          </form>
      </div>
    );
  }
  