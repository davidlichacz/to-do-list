from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

today = datetime.today().date()

weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
            4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

options = ["1) Today's tasks", "2) Week's tasks", "3) All tasks",
           "4) Add task", "0) Exit"]


def daily_tasks(day, date):
    tasks = session.query(Table).filter(Table.deadline == date).all()
    print(day, str(date.day), date.strftime('%b') + ':')
    if not tasks:
        print('Nothing to do!')
    else:
        for number, task in enumerate(tasks, 1):
            print(f'{number}. {task}')
    print('')


while True:
    print(*options, sep='\n')
    selection = int(input())
    if selection == 1:
        daily_tasks('Today', today)
    if selection == 2:
        for n in range(7):
            next_day = today + timedelta(days=n)
            daily_tasks(weekdays[next_day.weekday()], next_day)
    if selection == 3:
        all_tasks = session.query(Table.task, Table.deadline).order_by(Table.deadline).all()
        print('All tasks:')
        for number, task in enumerate(all_tasks, 1):
            print(f'{number}. {task[0]}. {task[1].day} {task[1].strftime("%b")}')
        print('')
    if selection == 4:
        print('Enter task')
        new_task = input()
        print('Enter deadline')
        deadline = datetime.strptime(input(), '%Y-%m-%d')
        new_row = Table(task=new_task, deadline=deadline)
        session.add(new_row)
        print('The task has been added!')
        session.commit()
    if selection == 0:
        print('Bye!')
        break
