from flask import Flask, request, jsonify
from calculations import compute_viu

app = Flask(__name__)

# Global storage (in-memory; use Redis/DB for prod)
materials = []

@app.route('/api/add_material', methods=['POST'])
def add_material():
    global materials
    data = request.json
    materials.append(data)
    return jsonify({"message": "Material added", "materials": materials})

@app.route('/api/compute_viu', methods=['POST'])
def compute():
    global materials
    data = request.json
    mat1_idx = int(data['mat1_idx'])
    mat2_idx = int(data['mat2_idx'])
    blend_pct1 = int(data['blend_pct1'])
    params = data['params']

    mat1 = materials[mat1_idx]
    mat2 = materials[mat2_idx]
    w1 = blend_pct1 / 100
    w2 = 1 - w1
    blended = {k: w1 * mat1.get(k, 0) + w2 * mat2.get(k, 0) for k in mat1 if k != "name"}
    blended['name'] = 'Blended'
    blended['price'] = w1 * mat1.get('price', 0) + w2 * mat2.get('price', 0)


    res1 = compute_viu(mat1, params)
    res2 = compute_viu(mat2, params)
    res_blend = compute_viu(blended, params)

    return jsonify({
        "res1": res1,
        "res2": res2,
        "res_blend": res_blend,
        "mat1_name": mat1["name"],
        "mat2_name": mat2["name"]
    })

@app.route('/api/materials', methods=['GET'])
def get_materials():
    return jsonify(materials)

if __name__ == '__main__':
    app.run(debug=True)
