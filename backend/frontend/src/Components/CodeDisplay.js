import hljs from 'highlight.js'; // npm install highlight.js
import 'highlight.js/styles/monokai.css'; 
import React, { useEffect } from 'react';

const CodeDisplay = React.forwardRef(({ code }, ref) => {
  useEffect(() => {
    // Reset any previous highlights before applying new highlights
    const codeElements = ref.current.querySelectorAll('pre code');
    codeElements.forEach((codeElement) => {
      codeElement.dataset.highlighted = ''; // Unset any previously highlighted status
    });
    
    // Apply highlight.js to all code blocks
    hljs.highlightAll();
  }, [code, ref]); // Re-run the effect when `code` or `ref` changes

  return (
    <div
      ref={ref} // Attach the ref here
      style={{
        border: '1px solid #ccc',
        borderRadius: '5px',
        padding: '10px',
        backgroundColor: '#2c2c2c',
        color: '#e0e0e0',
        height: '85%',
        width: '40%',
        margin: '10px 20px 10px 20px',
        overflowY: 'auto', // Ensure scrollable content
        fontFamily: 'monospace',
        textAlign: 'left',
      }}
    >
      <pre
        style={{
          margin: 0,
          whiteSpace: 'pre-wrap',
          wordWrap: 'break-word',
        }}
      >
        <code>{code}</code>
      </pre>
    </div>
  );
});

export default CodeDisplay;
