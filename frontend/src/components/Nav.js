const Nav = (createCookie, uploadImages, deleteImages, searchImage, setErrorLabel) => {
    return (
        <div style={navStyle}>

            <h2>Example Database</h2>
            <div style={uploadComboStyle}>
                <form encType="multipart/form-data" id="searchexamples-form" style={formStyle}>
                    <input type="file" id="searchexamples"/>
                </form>
                <button style={navButtonStyle} onClick={() => searchImage(true)}>Search</button>
            </div>


            <h2>Custom Database</h2>
            <div style={uploadComboStyle}>
                <form encType="multipart/form-data" id="uploadimages-form" style={formStyle}>
                    <input type="file" multiple id="uploadimages"/>
                </form>
                <button style={navButtonStyle} onClick={uploadImages}>Upload Images</button>
            </div>
            

            <div style={uploadComboStyle}>
                <form encType="multipart/form-data" id="searchimages-form" style={formStyle}>
                    <input type="file" id="searchimages"/>
                </form>
                <button style={navButtonStyle} onClick={() => searchImage(false)}>Search</button>
            </div>
            
            <div>
                <button onClick={deleteImages} style={{width:"100%"}}>Delete Corpus</button>
            </div>

      </div>
    );
};

const navStyle = {
  width: '25%',
  backgroundColor:'#ff4931',
  textAlign:"center",
  minHeight: '70vh'
}

const uploadComboStyle = {
    display: 'flex',
    justifyContent: 'space-between'
};

const formStyle = {
    width: '50%'
}

const navButtonStyle = {
    width: '25%',
    textAlign:"center"
}

export default Nav
