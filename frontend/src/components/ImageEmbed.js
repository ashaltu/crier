const testImgPath = "/home/ashaltu/crier/backend/tmp_corpus/dmcuorqdf7d1gomsgae8f8/sunflower.jpg"
const ImageEmbed = ({videoID, startTime}) => {
    const url = `/home/ashaltu/crier/backend/tmp_corpus/dmcuorqdf7d1gomsgae8f8/sunflower.jpg`
    return (
        <>
            <iframe
            src={url}
            title='User Image'
            />
        </>
    )
}

export default ImageEmbed
