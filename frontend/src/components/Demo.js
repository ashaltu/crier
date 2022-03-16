
const Demo = (createCookie, uploadImages, deleteImages, searchImage, insertImages) => {
    return (
        <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign: 'center',
          minHeight: '70vh'
        }}>

        
        <button onClick={createCookie}>Create Cookie</button>
        
        <form encType="multipart/form-data">
          <input type="file" multiple id="uploadimages"/>
        </form>
        
        <button onClick={uploadImages}>Upload Images</button>
        <button onClick={deleteImages}>Delete Images</button>

        <form encType="multipart/form-data">
          <input type="file" multiple id="searchimages"/>
        </form>
        
        <button onClick={searchImage}>Search Images</button>

        {insertImages()}

      </div>
    );
}

export default Demo