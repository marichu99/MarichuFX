import React from "react"

class DisplayTable extends React.Component{
    constructor(props){
        super(props)
        this.state={
            list:[]
        }
        this.callApi=this.callApi.bind(this)
        this.callApi();
    }
    callApi(){
        fetch("http://localhost:4444/getData",
        {
            method: "GET",
            mode: 'cors',
            headers:{
                "Content-Type":"Application/json"
            }

        }
        ).then(res=>res.json())
        .then(data=>{
            console.log(data)
            this.setState({
                list:data.data
            })
        })
    }
    render(){
        let tb_data= this.state.list.map((item)=>{
            return(
                <tr key={item.id}>
                    <td>{item.id}</td>
                    <td>{item.Symbol}</td>
                    <td>{item.Type}</td>
                    <td>{item.MultiTimeFrame}</td>
                </tr>
            )
        })
        return(
            <div>
                <table>
                    <thead>
                        <tr>
                        <th>ID</th>
                        <th>Symbol</th>
                        <th>Type</th>
                        <th>MultiTimeFrame</th>
                        <th>ID</th>
                        </tr>
                    </thead>
                    <tbody>
                    {tb_data}
                    </tbody>
                </table>
            </div>
        )
    }
}
export default DisplayTable;