const Header = () => {
    return (
        <>
            <h1 style={headingStyle}> CRIER</h1>
            <h2 style={subHeadingStyle}> Custom Reverse Image Extractions Ranked </h2>
        </>
    )
}

const headingStyle = {
    color:'White',
    backgroundColor:'#ff4931',
    textAlign:"center"
}

const subHeadingStyle = {
    color:'Grey',
    textAlign:"center"
}

export default Header
