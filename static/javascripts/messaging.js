const CSSTransition = ReactTransitionGroup.CSSTransition;
class Message extends React.Component{
    constructor(props){
        super(props);
        this.props = props;

        this.side = "right";
        this.d = "M 0,0 L 10,5 L 7,0 L 0,0";
        if(this.props.sender == 1){
            this.side = "left";
            this.d = "M 10,0 L 0,5 L 3,0 L 0,0";
        }

        this.state = {height:0, width:0, animation: false}
        this.tempMessageBoxRef = React.createRef();
        this.messageBoxRef = React.createRef();

    }

    componentDidMount(){
        //console.log(this.tempMessageBoxRef.current.offsetWidth, this.tempMessageBoxRef.current.offsetHeight)
        this.setState({animation: true, width: this.tempMessageBoxRef.current.offsetWidth, height: this.tempMessageBoxRef.current.offsetHeight})
    }

    beforeAnimation(){
        console.log(this.messageBoxRef.current)
        this.messageBoxRef.current.style.marginBottom = (this.state.height + 8).toString() + "px";
        document.getElementById("chatBox").scrollTop = document.getElementById("chatBox").scrollHeight;
    }

    duringAnimation(){
        this.messageBoxRef.current.style.marginBottom =  "8px";
        this.messageBoxRef.current.style.width = (this.state.width+1).toString() + "px";
        this.messageBoxRef.current.style.height = (this.state.height+1).toString() + "px";
    }

    render(){
        return(<div>
            {
                !this.state.animation?<div className={`messageBox`} ref={this.tempMessageBoxRef} >
                {this.props.message.includes('\n')?<NewlineText text={this.props.message}/>:this.props.message}
            </div>:<CSSTransition classNames="messageAnim"
            appear={true}
            enter={false}
            timeout={300}
            in={this.state.animation}
            onEnter={this.beforeAnimation.bind(this)}
            onEntering={this.duringAnimation.bind(this)}
            >
            <div className={`messageBox ${this.side}`} ref={this.messageBoxRef}>
                {this.props.message.includes('\n')?<NewlineText text={this.props.message}/>:this.props.message}
                <svg viewBox="0 0 10 5" className={`svgholder ${this.side}`}>
                    <path fill="#ffffff" d={this.d}/>
                </svg>
                
            </div>
            </CSSTransition>
            }
            
            </div>)
    }
}

class ChatBox extends React.Component{
    constructor(props){
        super(props);
        this.props = props;
    }

    render(){
        return(<div id="chatBox">
            {this.props.messages.map((values, index)=>{
                return <Message sender={values.sender} message={values.message} key={index}/>
            })
            }
        </div>)
    }
}

function NewlineText(props) {
    const text = props.text;
    return text.split('\n').map(str => <p>{str}</p>)
}

var chatMessages = []
ReactDOM.render(<ChatBox messages={chatMessages}/>, document.getElementById("holder"));