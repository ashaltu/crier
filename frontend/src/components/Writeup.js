import ReactMarkdown from 'react-markdown'
import rehypeRaw from 'rehype-raw'

const Writeup = (markdown) => {
    return (
        <div id='markdown' style={markdownStyle}>
            <ReactMarkdown rehypePlugins={[rehypeRaw]} children={markdown} />
        </div>
    );
}

const markdownStyle = {
    width: '65%'
}

export default Writeup
