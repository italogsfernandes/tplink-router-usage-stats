from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from models import Base, Device, DataUsageReading


def write_output_to_file(stats, created_date, output_file, output_file_completo):
    with open(output_file, "a+") as file:
        file.write("#"*80 + "\n")
        for stat in stats:
            print(f'{created_date.strftime("%D %T")} | {stat}')
            file.write(f'{created_date.strftime("%D %T")} | {stat}\n')
    
    with open(output_file_completo, "a+") as file:
        for stat in stats:
            file.write(f'{created_date.strftime("%D")}\t')
            file.write(f'{created_date.strftime("%T")}\t')
            file.write(f'{stat.ip}\t')
            file.write(f'{stat.mac.upper()}\t')
            file.write(f'{stat.total_byte}\t')
            file.write(f'{stat.apelido}\t')
            file.write(f'{stat.total_best_unit}\t')
            file.write(f'{stat.total_preco:.2f}\t')
            file.write('\n')


def save_output_in_database(stats, created_date):
    engine = create_engine('sqlite:///database.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    for stat in stats:
        device = get_or_create(session, Device, mac=stat.mac.upper())
            
        last_data_usage_reading = session.query(DataUsageReading).filter_by(
            device=device
        ).order_by(desc(DataUsageReading.created_date)).first()
        if last_data_usage_reading:
            # Se nova leitura for menor do que a antiga
            if stat.total_byte < last_data_usage_reading.total_byte:
                device.total_byte += last_data_usage_reading.total_byte

        data_usage_reading = DataUsageReading(
            created_date=created_date,
            device=device,
            total_byte=stat.total_byte,
        )
        session.add(data_usage_reading)
        session.commit()
    print("#"*80)
    print("# Dados salvos no banco de dados")
    print("#"*80)
    for device in session.query(Device).order_by(desc(Device.total_byte)):
        total_byte = device.get_full_total_byte(session)
        total_device = device.get_total_best_unit(total_byte)
        print(f"{device} | {total_device}")
    print("#"*80)

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance