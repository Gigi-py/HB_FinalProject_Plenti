
function Homepage(props) {
    return (
      <React.Fragment>
        <h1>Welcome to Balloonicorn's Trading Card Site!</h1>
        <a href="/cards">Go to the cards page</a>
        <img href="/static/img/balloonicorn.jpg" />
      </React.Fragment>
    );
  }
  
  ReactDOM.render(<Homepage />, document.getElementById('app'));