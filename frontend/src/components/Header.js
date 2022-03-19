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
    textAlign:"center",
    margin: 0,
    padding: '5px'
}

const subHeadingStyle = {
    color:'Grey',
    textAlign:"center",
    backgroundColor:'white',
    margin: 0,
    padding: '5px'
}

export default Header
