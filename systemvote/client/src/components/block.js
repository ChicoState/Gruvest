import React, { Component } from 'react';
import './block.css';

/* Component for individual messages */
class Block extends Component{
	/* Assigns callback event handlers from parent component */
	render(){
		this.id = this.props.msg.id;
		this.message = this.props.msg.message;
		this.upvotes = this.props.msg.upvotes;
		this.downvotes = this.props.msg.downvotes;
		this.ranking = this.props.msg.upvotes - this.props.msg.downvotes;
		this.upArrow = "./upvote_arrow.png";
		this.downArrow = "./downvote_arrow.png";
		return(
		<div id="block">
			<p className="rank">{this.ranking}</p>
			<h4 className="upvote" onClick={this.props.onUpClick}>&#9650;</h4>
			<p className="message">{this.message}</p>
			<h4 className="downvote" onClick={this.props.onDownClick}>&#9660;</h4>
		</div>
		);
	}
}

export default Block;