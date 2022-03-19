const ImagesBody = (insertImages, errorLabel) => {
    return (
        <div style={imagesBodyStyle}>
            {
                errorLabel && 
                <>
                    <h3 style={{width: '100%', textAlign: 'center'}}>{errorLabel}</h3>
                </>
            }
            {insertImages()}
        </div>
    );
};

const imagesBodyStyle = {
    display:'flex',
    flexWrap: 'wrap',
    width: '75%',
    justifyContent: 'space-evenly',
    alignItems: 'center'
  }

export default ImagesBody
