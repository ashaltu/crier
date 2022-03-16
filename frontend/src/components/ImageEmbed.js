const ImageEmbed = ({imgPath, distance}) => {
    let imgPathStack = imgPath.split("/");
    const imgName = imgPathStack.pop();
    const token = imgPathStack.pop();
    const imgUrl = `http://40.122.200.108:5001/${token}/${imgName}`;
    return (
        <>
            <img
            width="200"
            src={imgUrl}
            alt={imgName}
            />
        </>
    )
}

export default ImageEmbed
