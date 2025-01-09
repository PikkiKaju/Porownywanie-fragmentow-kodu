import React, { useState } from 'react';
import plus from './Plus.png';

const FileUploader = ({ files, onFileChange, onFileRemove }) => {
  return (
    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '20px', justifyContent: 'center', height: "250px"}}>
      <div>
        <label
          style={{
            display: 'inline-block',
            padding: '7px 15px 10px',
            backgroundColor: '#f44336',
            color: 'white',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          <img src={plus} style={{ width: '20px', height: '20px', marginRight: '5px', marginBottom: '-5px' }}/> Dodaj pliki
          <input
            type="file"
            multiple
            style={{ display: 'none' }}
            onChange={onFileChange}
          />
        </label>
      </div>

    <div>
        
        <div style={{ border: '1px solid white', padding: '0px 20px 10px', borderRadius: '5px', width: '450px', maxHeight: '200px', overflowY: 'auto' }}>
            {files.length > 0 ? (
            <ul style={{ listStyleType: 'none', padding: 0}}>
                {files.map((file, index) => (
                <li
                    key={index}
                    style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}
                >
                    <span style={{color: 'white'}}>{file.name}</span>
                    <button
                    onClick={() => onFileRemove(file.name)}
                    style={{
                        backgroundColor: '#f44336',
                        color: '#fff',
                        border: 'none',
                        borderRadius: '3px',
                        padding: '5px',
                        marginLeft: '20px',
                        cursor: 'pointer',
                    }}
                    >
                    ✖
                    </button>
                </li>
                ))}
            </ul>
            ) : (
            <p style={{color: '#767676'}}>Brak dodanych plików.</p>
            )}
            </div>
        </div>
    </div>
  );
};

export default FileUploader;
