function Scroll({ icon, onClick }) {
    return (
        <button
            style={{
                background: 'none',
                border: 'none',
                fontSize: '40px',
                cursor: 'pointer',
                padding: '0',
                color: '#f44336',
            }}
            onClick={onClick} // Attach the click handler here
        >
            {icon}
        </button>
    );
}

export default Scroll;