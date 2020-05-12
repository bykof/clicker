# Websocket Documentation

This is the websocket documentation for clicker.

## Click

Send a click to increase clicks of user 

### Endpoint

```
/game/click
```

#### Parameters

<table>
<thead>
    <tr>
        <th>Name</th>
        <th>Description</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>token</td>
        <td>The JWT-Token of the current logged in user</td>
    </tr>
</tbody>
</table>

### Events

#### On: `*`

Response: Added points.

```
{
    "points": 123 
}
```

---

## Generators

Adds and sends the generator's created clicks.

### Endpoint

```
/game/generators
```

#### Parameters

<table>
<thead>
    <tr>
        <th>Name</th>
        <th>Description</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>token</td>
        <td>The JWT-Token of the current logged in user</td>
    </tr>
</tbody>
</table>

### Scheduled

#### On: `Every second`

Response: The added points by the generators.

```
{
    "points": 123
}
```

---

## Balance

Sends the current balance of an user in an interval of 1 second.

### Endpoint

```
/game/balance
```

#### Parameters

<table>
<thead>
    <tr>
        <th>Name</th>
        <th>Description</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>token</td>
        <td>The JWT-Token of the current logged in user</td>
    </tr>
</tbody>
</table>

### Scheduled

#### On: `Every second`

Response: The current points balance.

```
{
    "points": 123
}
```