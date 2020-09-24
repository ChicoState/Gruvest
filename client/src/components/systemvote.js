import React, { Component } from 'react';
import './systemvote.css';
import Block from './block.js';

/* Compenent handling messages */
class Systemvote extends Component {
	constructor() {
		super();
		this.state = {
			messages: []
		};
		console.log('Init systemvote');
	}
	/* Establish pre-existing message blocks */
	componentDidMount() {
		console.log('start systemvote componentDidMount');
		fetch('/allmsgs')
		.then(response => {
			if (response.status !== 200) {
				console.log('allmsgs fetch problem - status code: ' + response.status);
				return;
			}
			response.json()
			.then(allmsgs => {
				console.log('allmsgs fetched:');
				console.log(allmsgs);
				this.setState({messages: allmsgs});
			});
		})
		.catch(err => {
			console.log('allmsgs fetch error :-S', err);
		});
		console.log('end systemvote componentDidMount');
	}
	/* If user hits return, insert new non-empty message into MySQL 
	 * and update message list */
	handleMessage(event){
		if(event.key !== 'Enter'){return;}
		const msg = event.target.value;
		console.log("msg is " + msg);
		if(msg === ""){return;}
		/* addmsg routine */
		fetch(`/addmsg?&message=${msg}`)
		.then(response => {
			if (response.status !== 200){
				console.log('addstat fetch problem - status code: ' + response.status);
				return;
			}
			response.json()
			.then(addmsg => {
				console.log('addmsg fetched:');
				console.log(addmsg);
				this.setState({messages: addmsg});
			});
		})
		.catch(err => {
			console.log('addstat fetch error :-S', err);
		});

		event.target.value = "";
	}
	/* Callback event handler to increment upvotes */
	handleUpVote(message){
		let id = message.id;
		let up = message.upvotes + 1;
		let dw = message.downvotes;
		
		fetch(`/updatemsg?upvotes=${up}&downvotes=${dw}&id=${id}`)
		.then(response => {
			if (response.status !== 200) {
				console.log('update fetch problem - status code: ' + response.status);
				return;
			}
			response.json()
			.then(updatemsg => {
				console.log('updatemsg fetched:');
				console.log(updatemsg);
				this.setState({messages: updatemsg});
			});
		})
		.catch(err => {
			console.log('updatemsg fetch error :-S', err);
		});
		
		/* Function to quicksort rankings, update list */
	}
	/* Callback event handler to increment downvotes */
	handleDownVote(message){
		let id = message.id;
		let up = message.upvotes;
		let dw = message.downvotes + 1;
		
		fetch(`/updatemsg?upvotes=${up}&downvotes=${dw}&id=${id}`)
		.then(response => {
			if (response.status !== 200) {
				console.log('update fetch problem - status code: ' + response.status);
				return;
			}
			response.json()
			.then(updatemsg => {
				console.log('updatemsg fetched:');
				console.log(updatemsg);
				this.setState({messages: updatemsg});
			});
		})
		.catch(err => {
			console.log('updatemsg fetch error :-S', err);
		});
		
		/* Function to quicksort rankings, update list */
	}
	
	render() {
		return (
		<div>
			<h2>Add New Messages</h2>
				<div onKeyDown={event => this.handleMessage(event)}>
					<input type='text' id='message' size = '100' placeholder="type your message here" autoFocus />
				</div>
			<h2>Vote</h2>
			{this.state.messages.map(message =>
				<ul>
					<li key={message.id}>
						<Block msg={message} onUpClick={() => this.handleUpVote(message)} 
							onDownClick={() => this.handleDownVote(message)}/>
					</li>
				</ul>
			)}
		</div>
		);
	}
}

export default Systemvote;
