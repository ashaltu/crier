const ImageEmbed = ({imgPath, distance, rank}) => {
    let imgPathStack = imgPath.split("/");
    const imgName = imgPathStack.pop();
    const token = imgPathStack.pop();
    const imgUrl = `https://crierapi.ashaltu.com/${token}/${imgName}`;
    return (
        <div style={imageEmbedStyle}>
            <img
            height="200"
            src={imgUrl}
            alt={imgName}
            style={imgStyle}
            />
            <h3 style={metricStuff}>Rank: {rank}</h3>
            <h3 style={metricStuff}>Similarity: {distance.toFixed(4)}</h3>
        </div>
    )
}

const imageEmbedStyle = {
    // Nothing i guess
}

const metricStuff = {
    textAlign: 'center'
}

const imgStyle = {
    margin: 10
}

export default ImageEmbed
