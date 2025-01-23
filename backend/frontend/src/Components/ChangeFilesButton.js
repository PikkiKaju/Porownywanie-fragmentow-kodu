function ChangeFilesButton({ onPreviousFile, onNextFile, currentFileIndex, totalFiles }) {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        backgroundColor: '#f44336',
        borderRadius: '10px',
        width: '70%',
        padding: '10px 15px',
      }}
    >
      <button
        style={{
          background: 'none',
          border: 'none',
          fontSize: '20px',
          cursor: 'pointer',
          padding: '0',
          color: '#6a64ae',
        }}
        onClick={onPreviousFile}
      >
        ⮜
      </button>

      <span
        style={{
          fontSize: '16px',
          fontWeight: 'bold',
          color: 'white',
        }}
      >
        {currentFileIndex + 1}/{totalFiles}
      </span>

      <button
        style={{
          background: 'none',
          border: 'none',
          fontSize: '20px',
          cursor: 'pointer',
          padding: '0',
          color: '#6a64ae',
        }}
        onClick={onNextFile}
      >
        ⮞
      </button>
    </div>
  );
}

export default ChangeFilesButton;