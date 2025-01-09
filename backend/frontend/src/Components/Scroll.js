function Scroll({icon}){

    return(
        <button 
                  style={{
                  background: 'none',
                  border: 'none',
                  fontSize: '40px',
                  cursor: 'pointer',
                  padding: '0',
                  color: '#f44336',
                }}>
                {icon}
                </button>
    );
}

export default Scroll