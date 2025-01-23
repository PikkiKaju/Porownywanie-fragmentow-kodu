function DropDown({value, onChange, options }) {
    return (
        <div style={{position: 'relative', width: '100%' }}>
        <select
            value={value}
            onChange={onChange}
            style={{
                width: '70%',
                padding: '10px',
                fontSize: '16px',
                borderRadius: '10px',
                border: '1px solid white',
                backgroundColor: '#202124',
                color: 'white',
                cursor: 'pointer',
            }}
        >       
                {options.map((option, index) => (
                    <option key={index} value={option}>{option}</option>
                ))}
            </select>
        </div>
    );
};

export default DropDown;