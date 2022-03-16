import ReactMarkdown from 'react-markdown'

const Writeup = (markdown) => {
    return (
        <div id='markdown'>
            <ReactMarkdown children={markdown} />
        </div>
    );
}

export default Writeup
