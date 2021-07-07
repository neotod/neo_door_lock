def get_new_vals(from_vals):
    new_vals = []
    for val in from_vals:
        
        if type(val) == str:
            new_val = f'{val}_new'
        elif type(val) == int:
            new_val = val+1
        else:
            new_val = None
            
        new_vals.append(new_val)

    return new_vals