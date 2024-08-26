from flask import Flask, request, jsonify
from sqlalchmy import create_engine
from sqlalchemy.orm import sessionmaker
import services
import config
import model
import orm 
import repository

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)

def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    line = model.OrderLine(
        request.json["orderid"],
        request.json["sku"],
        request.json["qty"],
    )
    
    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, model.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"batchref": batchref}), 201
