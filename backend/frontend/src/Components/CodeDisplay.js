import hljs from 'highlight.js'; // npm install highlight.js
import 'highlight.js/styles/monokai.css'; 
import React, { useEffect }from 'react';

function CodeDisplay({code}){
    useEffect(() => {
        hljs.highlightAll();
      }, []);

    return(
        <div style={{
            border: '1px solid #ccc',
            borderRadius: '5px',
            padding: '10px',
            backgroundColor: '#2c2c2c',
            color: '#e0e0e0',
            height: '85%',
            width: '40%',
            margin: '10px 20px 10px 20px',
            overflowY: 'auto',
            fontFamily: 'monospace',
            textAlign: 'left'
        }}>
        <pre style={{
            margin: 0,
            whiteSpace: 'pre-wrap',
            wordWrap: 'break-word',
        }}>
        <code>{code}</code>
        </pre>
      </div>
    );
  };


export default CodeDisplay