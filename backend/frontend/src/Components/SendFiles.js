import React, { useState } from 'react';

const SendFiles = () => {
    const [buttonColor, setButtonColor] = useState('#f44336');

    return (
    <div style={{
        display: 'flex',
        width: '100%',     
        justifyContent: 'center' , 
        }}>
        <button
            type="submit"
            style={{
            backgroundColor: buttonColor,
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            padding: '0px 25px 0px 25px',
            cursor: 'pointer',
            }}
        onMouseEnter={() => setButtonColor('#6a64ae')} // Ciemniejszy odcień czerwieni
        onMouseLeave={() => setButtonColor('#f44336')} // Przywracamy oryginalny kolor
        >
            <h2>PRZEŚLIJ PLIKI</h2>
            </button>
        </div>
    );
};

export default SendFiles;